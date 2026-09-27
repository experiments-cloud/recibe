(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (ontable c)
    (on a d)
    (on b f)
    (on d b)
    (on e c)
    (on f e)
    (clear a)
    (handempty)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
    (on e f)
    (on f a)
  ))
)
