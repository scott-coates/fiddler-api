from django_rq import job


@job('default')
def discover_engagement_opportunities_from_batch_assignments_task(batch_id, assigned_eas):
  log_message = ("batch_id: %s", batch_id)

  with log_wrapper(logger.debug, *log_message):
    discovery_network = service.get_discovery_network_from_batch_assignments(assigned_eas)

    for recent_connection in discovery_network:
      external_id_ = recent_connection[constants.EXTERNAL_ID]
      provider_type = recent_connection[constants.PROVIDER_TYPE]
      populate_prospect_from_provider_info_chain.delay(external_id_, provider_type)
